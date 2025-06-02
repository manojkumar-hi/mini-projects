const imageInput = document.getElementById('imageInput');
const memeImage = document.getElementById('memeImage');
const topTextDiv = document.getElementById('topText');
const bottomTextDiv = document.getElementById('bottomText');
const memeArea = document.getElementById('memeArea');
const topTextInput = document.getElementById('topTextInput');
const bottomTextInput = document.getElementById('bottomTextInput');
const topFontSize = document.getElementById('topFontSize');
const bottomFontSize = document.getElementById('bottomFontSize');
const topFontColor = document.getElementById('topFontColor');
const bottomFontColor = document.getElementById('bottomFontColor');
const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const memeCanvas = document.getElementById('memeCanvas');

imageInput.addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(event) {
    memeImage.src = event.target.result;
  };
  reader.readAsDataURL(file);
});

// Sync text input with meme text divs
topTextInput.addEventListener('input', () => {
  topTextDiv.textContent = topTextInput.value;
});
bottomTextInput.addEventListener('input', () => {
  bottomTextDiv.textContent = bottomTextInput.value;
});

// Sync font size and color
function updateTextStyle(div, sizeInput, colorInput) {
  div.style.fontSize = sizeInput.value + 'px';
  div.style.color = colorInput.value;
}
[topFontSize, topFontColor].forEach(el => el.addEventListener('input', () => updateTextStyle(topTextDiv, topFontSize, topFontColor)));
[bottomFontSize, bottomFontColor].forEach(el => el.addEventListener('input', () => updateTextStyle(bottomTextDiv, bottomFontSize, bottomFontColor)));

// Initial style
updateTextStyle(topTextDiv, topFontSize, topFontColor);
updateTextStyle(bottomTextDiv, bottomFontSize, bottomFontColor);

// Drag and drop for meme text
function makeDraggable(el) {
  let offsetX, offsetY, isDragging = false;

  el.addEventListener('mousedown', function(e) {
    isDragging = true;
    const rect = el.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;
    el.style.zIndex = 10;
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    const areaRect = memeArea.getBoundingClientRect();
    let left = e.clientX - areaRect.left - offsetX;
    let top = e.clientY - areaRect.top - offsetY;

    // Boundaries
    left = Math.max(0, Math.min(left, memeArea.offsetWidth - el.offsetWidth));
    top = Math.max(0, Math.min(top, memeArea.offsetHeight - el.offsetHeight));

    el.style.left = left + 'px';
    el.style.top = top + 'px';
    el.style.transform = 'none';
  });

  document.addEventListener('mouseup', function() {
    isDragging = false;
    el.style.zIndex = '';
    document.body.style.userSelect = '';
  });
}

makeDraggable(topTextDiv);
makeDraggable(bottomTextDiv);

// Generate meme on canvas
generateBtn.addEventListener('click', function() {
  if (!memeImage.src) {
    alert('Please upload an image!');
    return;
  }
  const ctx = memeCanvas.getContext('2d');
  // Clear canvas
  ctx.clearRect(0, 0, memeCanvas.width, memeCanvas.height);

  // Draw image
  ctx.drawImage(memeImage, 0, 0, memeCanvas.width, memeCanvas.height);

  // Draw texts
  [topTextDiv, bottomTextDiv].forEach(div => {
    const style = window.getComputedStyle(div);
    ctx.font = `${style.fontWeight} ${parseInt(style.fontSize)}px Arial`;
    ctx.fillStyle = style.color;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.shadowColor = "#000";
    ctx.shadowBlur = 6;

    // Calculate position relative to memeArea
    const areaRect = memeArea.getBoundingClientRect();
    const divRect = div.getBoundingClientRect();
    const x = divRect.left - areaRect.left;
    const y = divRect.top - areaRect.top;

    ctx.fillText(div.textContent, x, y + 2);
    ctx.shadowBlur = 0;
  });

  memeCanvas.style.display = 'block';
  downloadBtn.disabled = false;
});

// Download meme
downloadBtn.addEventListener('click', function() {
  const link = document.createElement('a');
  link.download = 'meme.png';
  link.href = memeCanvas.toDataURL('image/png');
  link.click();
});