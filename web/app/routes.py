import pymssql
from app import app, db
from app import forms
from app import mssql
from flask import render_template, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    mssql.close_conn()
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            mssql.set_conn(
                server=form.server.data,
                user=form.username.data,
                password=form.password.data,
                dbname=form.dbname.data)
            if not user:
                user = User(
                    server=form.server.data,
                    username=form.username.data,
                    password=form.password.data,
                    dbname=form.dbname.data)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('workers_api')
            return redirect(next_page)
        except pymssql.OperationalError:
            flash('Invalid connection data')
            return redirect(url_for('login'))
        except pymssql.InterfaceError:
            flash('Connection to the database failed for an unknown reason')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In | Shop database ', form=form)


class WorkerAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'workers.html'
    context = {
        'title': 'Workers | Shop database',
        'table_name': 'Workers',
    }

    @staticmethod
    def get_workers() -> list:
        storage = mssql.WorkersStorage.get_connection(
            conn=mssql.get_conn())
        return storage.get_workers()

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.update_worker(
                    worker_id=request.form['worker_id'],
                    fullname=form.fullname.data,
                    salary=form.salary.data,
                    job=form.job.data,
                    address=form.address.data,
                    passport_number=form.passport_number.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f'Information about worker {form.fullname.data} was successfully updated.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting values into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_worker(worker_id=request.form['worker_id'])
        self.context['message'] = f'Successfully delete worker {form.fullname.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.add_worker(
                    fullname=form.fullname.data,
                    salary=form.salary.data,
                    job=form.job.data,
                    address=form.address.data,
                    passport_number=form.passport_number.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f'Worker {form.fullname.data} was successfully added to database.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash("Error on inserting values into table.")
        else:
            flash("Invalid form data.")

    def get(self):
        self.context['form'] = forms.WorkerForm()
        self.context['workers'] = WorkerAPI.get_workers()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.WorkersStorage.get_connection(
            conn=mssql.get_conn())
        form = forms.WorkerForm()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['workers'] = storage.get_workers()
        return render_template(self.template, **self.context)


class SupplierAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'suppliers.html'
    context = {
        'title': 'Suppliers | Shop database',
        'table_name': 'Suppliers',
    }

    @staticmethod
    def get_suppliers() -> list:
        storage = mssql.SuppliersStorage.get_connection(
            conn=mssql.get_conn())
        return storage.get_suppliers()

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.update_supplier(
                    supplier_id=request.form['supplier_id'],
                    name=form.name.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f'Information about supplier {form.name.data} was successfully updated.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting values into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_supplier(supplier_id=request.form['supplier_id'])
        self.context['message'] = f'Successfully delete supplier {form.name.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.add_supplier(
                    name=form.name.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                self.context['message'] = f'Supplier {form.name.data} was successfully added to database.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting values into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = forms.SupplierForm()
        self.context['suppliers'] = SupplierAPI.get_suppliers()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.SuppliersStorage.get_connection(
            conn=mssql.get_conn())
        form = forms.SupplierForm()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['suppliers'] = storage.get_suppliers()
        return render_template(self.template, **self.context)


class ProductAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'products.html'
    context = {
        'title': 'Products | Shop database',
        'table_name': 'Products',
    }

    @staticmethod
    def get_products() -> list:
        storage = mssql.ProductsStorage.get_connection(
            conn=mssql.get_conn())
        return storage.get_products()

    @staticmethod
    def get_form() -> forms.CustomerForm:
        form = forms.ProductForm()

        storage = mssql.ProducersStorage.get_connection(
            conn=mssql.get_conn())
        producers_choices = list(enumerate(storage.get_producers_names()))
        form.producer.choices = producers_choices

        storage = mssql.SuppliersStorage.get_connection(
            conn=mssql.get_conn())
        suppliers_choices = list(enumerate(storage.get_suppliers_names()))
        form.supplier.choices = suppliers_choices

        return form

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.update_product(
                    product_id=request.form['product_id'],
                    name=form.name.data,
                    quantity=form.quantity.data,
                    price=form.price.data,
                    promotion=form.promotion.data,
                    supplier=form.supplier.choices[form.supplier.data][1],
                    producer=form.producer.choices[form.producer.data][1])
                self.context['message'] = f'Information about product {form.name.data} was successfully updated.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_product(product_id=request.form['product_id'])
        self.context['message'] = f'Successfully delete product {form.name.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.add_product(
                    name=form.name.data,
                    quantity=form.quantity.data,
                    price=form.price.data,
                    promotion=form.promotion.data,
                    supplier=form.supplier.choices[form.supplier.data][1],
                    producer=form.producer.choices[form.producer.data][1])
                self.context['message'] = f'Product {form.name.data} was successfully added to database.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = ProductAPI.get_form()
        self.context['products'] = ProductAPI.get_products()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.ProductsStorage.get_connection(
            conn=mssql.get_conn())
        form = ProductAPI.get_form()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['products'] = storage.get_products()
        return render_template(self.template, **self.context)


class CustomerAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'customers.html'
    context = {
        'title': 'Customers | Shop database',
        'table_name': 'Customers'
    }

    @staticmethod
    def get_customers() -> list:
        storage = mssql.CustomersStorage().get_connection(
            conn=mssql.get_conn())
        return storage.get_customers()

    @staticmethod
    def get_form() -> forms.CustomerForm:
        cards_storage = mssql.DiscountCardsStorage().get_connection(
            conn=mssql.get_conn())
        choices = [(0, '-')] + [
            (i + 1, str(card_id))
            for i, card_id in enumerate(cards_storage.get_cards_ids())
        ]
        form = forms.CustomerForm()
        form.card_id.choices = choices
        return form

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                choice = form.card_id.data
                card_id = form.card_id.choices[choice][1] if choice else "NULL"
                storage.update_customer(
                    customer_id=request.form['customer_id'],
                    fullname=form.fullname.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data,
                    card_id=card_id)
                message = f'Information about customer {form.fullname.data} was successfully updated.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_customer(customer_id=request.form['customer_id'])
        self.context['message'] = f'Successfully delete customer {form.fullname.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                choice = form.card_id.data
                card_id = form.card_id.choices[choice][1] if choice else "NULL"
                storage.add_customer(
                    fullname=form.fullname.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data,
                    card_id=card_id)
                self.context['message'] = f'Customer {form.fullname.data} was successfully added to database.'
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = CustomerAPI.get_form()
        self.context['customers'] = CustomerAPI.get_customers()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.CustomersStorage().get_connection(
            conn=mssql.get_conn())
        form = CustomerAPI.get_form()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['customers'] = storage.get_customers()
        return render_template(self.template, **self.context)


class DiscountCardAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'discount_cards.html'
    context = {
        'title': 'Discount cards | Shop database',
        'table_name': 'Discount cards',
    }

    @staticmethod
    def get_cards() -> list:
        storage = mssql.DiscountCardsStorage().get_connection(
            conn=mssql.get_conn())
        return storage.get_cards()

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.update_card(
                    card_id=request.form['card_id'],
                    discount=form.discount.data,
                    start_date=form.start_date.data,
                    expiration=form.expiration.data)
                message = f'Information about card with {form.discount.data * 100}% discount was successfully updated.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_card(card_id=request.form['card_id'])
        self.context['message'] = f'Successfully delete discount card {form.discount.data * 100}% from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.add_card(
                    discount=form.discount.data,
                    start_date=form.start_date.data,
                    expiration=form.expiration.data)
                message = f'Discount card {form.discount.data * 100}% was successfully added to database.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = forms.DiscountCardForm()
        self.context['cards'] = DiscountCardAPI.get_cards()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.DiscountCardsStorage.get_connection(
            conn=mssql.get_conn())
        form = forms.DiscountCardForm()
        self.context['form'] = forms.DiscountCardForm()
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['cards'] = storage.get_cards()
        return render_template(self.template, **self.context)


class ProducerAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'producers.html'
    context = {
        'title': 'Producers | Shop database',
        'table_name': 'Producers',
    }

    @staticmethod
    def get_producers() -> list:
        storage = mssql.ProducersStorage().get_connection(
            conn=mssql.get_conn())
        return storage.get_producers()

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.update_producer(
                    producer_id=request.form['producer_id'],
                    name=form.name.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                message = f'Information about producer {form.name.data} was successfully updated.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_producer(producer_id=request.form['producer_id'])
        self.context['message'] = f'Successfully delete producer {form.fullname.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                storage.add_producer(
                    name=form.name.data,
                    address=form.address.data,
                    telephone=form.telephone.data,
                    email=form.email.data)
                message = f'Producer {form.name.data} was successfully added to database.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = forms.ProducerForm()
        self.context['producers'] = ProducerAPI.get_producers()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.ProducersStorage.get_connection(
            conn=mssql.get_conn())
        form = forms.ProducerForm()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['producers'] = storage.get_producers()
        return render_template(self.template, **self.context)


class PurchaseAPI(MethodView):
    decorators = [login_required, mssql.check_conn]
    template = 'purchases.html'
    context = {
        'title': 'Purchases | Shop database',
        'table_name': 'Purchases',
    }

    @staticmethod
    def get_purchases() -> list:
        storage = mssql.PurchasesStorage().get_connection(
            conn=mssql.get_conn())
        return storage.get_purchases()

    @staticmethod
    def get_form() -> forms.PurchaseForm:
        form = forms.PurchaseForm()

        storage = mssql.ProductsStorage.get_connection(
            conn=mssql.get_conn())
        products_choices = [(i, str(_id)) for i, _id in enumerate(storage.get_products_ids())]
        form.product_id.choices = products_choices

        storage = mssql.CustomersStorage.get_connection(
            conn=mssql.get_conn())
        customers_choices = [(i, str(_id)) for i, _id in enumerate(storage.get_customers_ids())]
        form.customer_id.choices = customers_choices

        storage = mssql.WorkersStorage.get_connection(
            conn=mssql.get_conn())
        workers_choices = [(0, '-')] + [(i + 1, str(_id)) for i, _id in enumerate(storage.get_workers_ids())]
        form.worker_id.choices = workers_choices

        return form

    def update(self, storage, form):
        if form.validate_on_submit():
            try:
                worker_num = form.worker_id.data
                worker_id = form.worker_id.choices[worker_num][1] if worker_num else "NULL"
                storage.update_purchase(
                    purchase_id=request.form['purchase_id'],
                    total_cost=form.total_cost.data,
                    quantity=form.quantity.data,
                    date=form.date.data,
                    product_id=form.product_id.choices[form.product_id.data][1],
                    customer_id=form.customer_id.choices[form.customer_id.data][1],
                    worker_id=worker_id)
                message = f'Information about purchase on total cost {form.total_cost.data} was successfully updated.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, storage, form):
        storage.delete_purchase(purchase_id=request.form['purchase_id'])
        self.context['message'] = f'Successfully delete purchase on total cost {form.total_cost.data} from database.'

    def add(self, storage, form):
        if form.validate_on_submit():
            try:
                worker_num = form.worker_id.data
                worker_id = form.worker_id.choices[worker_num][1] if worker_num else 'NULL'
                storage.add_purchase(
                    total_cost=form.total_cost.data,
                    quantity=form.quantity.data,
                    date=form.date.data,
                    product_id=form.product_id.choices[form.product_id.data][1],
                    customer_id=form.customer_id.choices[form.customer_id.data][1],
                    worker_id=worker_id)
                message = f'Purchase on total cost {form.total_cost.data} was successfully added to database.'
                self.context['message'] = message
            except (pymssql.OperationalError, pymssql.InterfaceError, pymssql.IntegrityError):
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = PurchaseAPI.get_form()
        self.context['purchases'] = PurchaseAPI.get_purchases()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        storage = mssql.PurchasesStorage.get_connection(
            conn=mssql.get_conn())
        form = PurchaseAPI.get_form()
        self.context['form'] = form
        self.context['message'] = ''
        if request.form['submit'] == 'Add':
            self.add(storage, form)
        if request.form['submit'] == 'Update':
            self.update(storage, form)
        if request.form['submit'] == 'Delete':
            self.delete(storage, form)
        self.context['purchases'] = storage.get_purchases()
        return render_template(self.template, **self.context)


app.add_url_rule('/workers/',
                 view_func=WorkerAPI.as_view('workers_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/suppliers/',
                 view_func=SupplierAPI.as_view('suppliers_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/products/',
                 view_func=ProductAPI.as_view('products_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/customers/',
                 view_func=CustomerAPI.as_view('customer_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/discount_cards/',
                 view_func=DiscountCardAPI.as_view('discount_card_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/producers/',
                 view_func=ProducerAPI.as_view('producer_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/purchases/',
                 view_func=PurchaseAPI.as_view('purchase_api'),
                 methods=['POST', 'GET'])
