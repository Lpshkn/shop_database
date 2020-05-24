function main() {
    const table = document.getElementById('table');

    for (let i = 1; i <= table.rows.length; i++) {
        document.getElementById(`del_img_${i}`).style.display = "none";
        document.getElementById(`upd_img_${i}`).style.display = "none";
    }
}

function showImages(row_index) {
    document.getElementById(`del_img_${row_index}`).style.display = "";
    document.getElementById(`upd_img_${row_index}`).style.display = "";
}

function hideImages(row_index) {
    document.getElementById(`del_img_${row_index}`).style.display = "none";
    document.getElementById(`upd_img_${row_index}`).style.display = "none";
}

function fillDeleteModal(id) {
    const eChildren = document.getElementById(id).children;
    const customer_id = eChildren[1].children[0].innerHTML;
    const fullname = eChildren[2].innerHTML;
    document.querySelector('input#del_id').value = customer_id;
    document.querySelector('p#del_info').innerHTML = `Are you sure that you want remove ${fullname}?` +
        `This action cannot be canceled.`
}

function fillUpdateModal(id) {
    const eChildren = document.getElementById(id).children;

    document.querySelectorAll('input#fullname.form-control')[1].value = eChildren[2].innerHTML;
    document.querySelectorAll('input#address.form-control')[1].value = eChildren[4].innerHTML;
    document.querySelectorAll('input#email.form-control')[1].value = eChildren[5].innerHTML;
    document.querySelectorAll('input#telephone.form-control')[1].value = eChildren[6].innerHTML;

    document.querySelector('input#upd_id').value = eChildren[1].children[0].innerHTML;

    const val = eChildren[3].innerHTML;
    const sel = document.querySelectorAll('select#card_id.form-control')[1];
    const opts = sel.options;

    for (let j = 0;; j++) {
        if (opts[j].value === val) {
            sel.selectedIndex = j;
            break;
        }
    }

}