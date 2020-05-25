function fillDeleteModal(id) {
    const eChildren = document.getElementById(id).children;
    const customer_id = eChildren[1].children[0].innerHTML;
    const fullname = eChildren[2].innerHTML;
    document.querySelector('input#del_id').value = customer_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want remove ${fullname}?` +
        ` This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const eChildren = document.getElementById(id).children;

    document.querySelectorAll('input#fullname.form-control')[1].value = eChildren[2].innerHTML;
    document.querySelectorAll('input#salary.form-control')[1].value = eChildren[3].innerHTML;
    document.querySelectorAll('input#job.form-control')[1].value = eChildren[4].innerHTML;
    document.querySelectorAll('input#address.form-control')[1].value = eChildren[5].innerHTML;
    document.querySelectorAll('input#email.form-control')[1].value = eChildren[8].innerHTML;
    document.querySelectorAll('input#telephone.form-control')[1].value = eChildren[7].innerHTML;
    document.querySelectorAll('input#passport_number.form-control')[1].value = eChildren[6].innerHTML;

    document.querySelector('input#upd_id').value = eChildren[1].children[0].innerHTML;
}