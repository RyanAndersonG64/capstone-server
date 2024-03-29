const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Declaring the array of image filenames */
const pics = ['pic1.jpg', 'pic2.jpg', 'pic3.jpg', 'pic4.jpg', 'pic5.jpg'];
/* Declaring the alternative text for each image file */
const alttext =['Closeup of a human eye','Rock that looks like a wave','Purple and white pansies','Section of wall from a pharoahs tomb','Large moth on a leaf'];
/* Looping through images */
for (let i = 0; i < pics.length; i++) {
const newImage = document.createElement('img');                  
newImage.setAttribute('src', pics[i]);
newImage.setAttribute('alt', alttext[i]);
thumbBar.appendChild(newImage);
}
thumbBar.addEventListener('click', e => {
    displayedImage.src = e.target.src;
    displayedImage.alt = e.target.alt;});
/* Wiring up the Darken/Lighten button */
btn.addEventListener('click', () => {
    const buttonstate = btn.getAttribute('class');
    if (buttonstate == 'dark') {
      btn.setAttribute('class','light');
      btn.textContent = 'Lighten';
      overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    } else {
      btn.setAttribute('class','dark');
      btn.textContent = 'Darken';
      overlay.style.backgroundColor = 'rgba(0,0,0,0)';
    }
  });