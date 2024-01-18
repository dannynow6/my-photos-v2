// clear local storage when form submitted
const submitBtn = document.getElementById('photoFormSubmit')

const ClearStorage = () => {
  if (localStorage) {
    clearLocalStorage()
  }
}
submitBtn.addEventListener('click', ClearStorage())

// Attach event listener to the form's submit event
const form = document.getElementById('PhotoForm')
if (form) {
  form.addEventListener('submit', function (event) {
    // You might want to check here if the form submission is valid
    // before clearing the local storage
    clearLocalStorage()
  })
}

// clear local storage when form submitted
const submitBtn = document.getElementsByName('add_photo_submit')
submitBtn.addEventListener('click', function () {
  if (localStorage) {
    clearLocalStorage()
  }
})

// Example function to save form data to local storage
function saveFormData () {
  const formData = {}
  document
    .querySelectorAll(
      '#id_title',
      '#id_description',
      '#id_location',
      '#id_camera',
      '#id_keywords'
    )
    .forEach(input => {
      formData[input.name] = input.value
    })
  localStorage.setItem('formData', JSON.stringify(formData))
}

// Example function to repopulate form with saved data
function repopulateFormData () {
  const savedData = JSON.parse(localStorage.getItem('formData'))
  if (savedData) {
    Object.keys(savedData).forEach(key => {
      const input = document.querySelector(`#yourForm [name="${key}"]`)
      if (input) input.value = savedData[key]
    })
  }
}

// Call this function on page load
document.addEventListener('DOMContentLoaded', repopulateFormData)

// Example function to clear saved form data
function clearFormData () {
  localStorage.removeItem('formData')
}

// Attach this function to your form's submit event
document.querySelector('#yourForm').addEventListener('submit', clearFormData)
