const customName = document.getElementById('customname');
const randomize = document.querySelector('.randomize');
const story = document.querySelector('.story');

function randomValueFromArray(array){
  const random = Math.floor(Math.random()*array.length);
  return array[random];
}

const storyText = "It was 94 degrees fahrenheit outside, so :insertx: went for a walk. When they got to :inserty:, they stared in horror for a few moments, then :insertz:. Bob saw the whole thing, but was not surprised — :insertx: weighs 300 pounds, and it was a hot day.";
const insertX = ["Willy the Goblin", "Big Daddy", "Father Christmas"];
const insertY = ["the soup kitchen", "Disneyland", "the White House"];
const insertZ = ["spontaneously combusted", "melted into a puddle on the sidewalk", "turned into a slug and crawled away"];

randomize.addEventListener('click', result);

function result() {
  let newStory = storyText;

  const xItem = randomValueFromArray(insertX);
  newStory = newStory.replaceAll(":insertx:" , xItem);

  const yItem = randomValueFromArray(insertY);
  newStory = newStory.replace(":inserty:" , yItem);
  
  const zItem = randomValueFromArray(insertZ);
  newStory = newStory.replace(":insertz:" , zItem);

  if(customName.value !== '') {
    const Name = customName.value;
    newStory = newStory.replace("Bob" , Name);
  }

  if(document.getElementById("uk").checked) {
    let weight = Math.round(300/14);
    let temperature =  Math.round(62*5/9)
    newStory = newStory.replace("94" , temperature);
    newStory = newStory.replace("degrees Fahrenheit" , "degrees Centigrade");
    newStory = newStory.replace("300" , weight);
    newStory = newStory.replace("pounds" , "stone");
  }

  story.textContent = newStory;
  story.style.visibility = 'visible';
}