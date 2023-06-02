const splashScreen = document.getElementById('splashscreen')

document.addEventListener('keydown', () => {
    splashScreen.classList.add('hidden')
})

const nextBtn = document.querySelector('.next-btn')

nextBtn.addEventListener('click', (e) => {
    e.preventDefault()

    let firstForm = new FormData(document.querySelector('form'))
    fetch('/users/providers/first_form', { method : 'POST', body : firstForm})
        .then(r => r.json())
        .then(d => {
            const errorDiv1 = document.querySelector('.error-field-1')
            errorDiv1.innerHTML = ''
            if (d.length > 0){
                for (let i in d)
                    errorDiv1.innerHTML += `
                    <p> ${d[i]} </p>
                    `
            } else {
                document.querySelector('.second-form').classList.add('slidefromright')
                document.querySelector('.first-form').classList.add('slidetoleft')
            }
        })
})


