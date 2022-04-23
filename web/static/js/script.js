function checkInputsNum(name) {
  const email = document.getElementById(name);
  const emailValue = email.value.trim();
  var num = /[0-9]/g;
  if(emailValue === '') {
    setErrorFor(email, 'Pole nemůže být prázdné.');
  } else if (!emailValue.match(num)) {
    setErrorFor(email, 'Zadej číslo.');
  } else {
    setSuccessFor(email);
  }
}
function checkInputsNum1(name) {
  const email = document.getElementById(name);
  const emailValue = email.value.trim();
  var num = /[0-9]/g;
  if(emailValue === '') {
    setErrorFor1(email, 'Pole nemůže být prázdné.');
  } else if (!emailValue.match(num)) {
    setErrorFor1(email, 'Zadej číslo.');
  } else {
    setSuccessFor1(email);
  }
}
function checkInputsEmpty(name) {
  const email = document.getElementById(name);
  const emailValue = email.value.trim();
  if(emailValue === '') {
    setErrorFor(email, 'Pole nemůže být prázdné.');
  } else {
    setSuccessFor(email);
  }
}
function setErrorFor(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector('small');
	formControl.className = 'form-control error';
	small.innerText = message;
}
function setSuccessFor(input) {
	const formControl = input.parentElement;
	formControl.className = 'form-control success';
}
function setErrorFor1(input, message) {
	const formControl = input.parentElement;
	const small = formControl.querySelector('small');
	formControl.className = 'form-control1 error';
	small.innerText = message;
}
function setSuccessFor1(input) {
	const formControl = input.parentElement;
	formControl.className = 'form-control1 success';
}

function markOnClick(elem) {
  var checkbox = elem.querySelector('td>input');
  checkbox.checked = !checkbox.checked;
  if(checkbox.checked) {
    elem.style.backgroundColor = '#5ED668';
    elem.style.transform = 'scale(1.02)';
    elem.style.boxShadow =  '2px 2px 12px rgba(0, 0, 0, 0.2), -1px -1px 8px rgba(0, 0, 0, 0.2)';
  } else {
    elem.style.backgroundColor = '';
    elem.style.transform = 'scale(1)';
    elem.style.boxShadow =  '2px 2px 12px rgba(0, 0, 0, 0), -1px -1px 8px rgba(0, 0, 0, 0)';
  }
}