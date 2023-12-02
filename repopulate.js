// Example function to save form data to local storage
function saveFormData () {
  const formData = {}
  document
    .querySelectorAll('#yourForm input, #yourForm select')
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
