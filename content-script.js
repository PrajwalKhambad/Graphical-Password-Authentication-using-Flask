const extensionUrl = chrome.runtime.getURL("popup.html");

const container = document.createElement('div');
container.setAttribute('id', 'my-extension-container');
document.body.appendChild(container);

fetch(extensionUrl)
  .then(response => response.text())
  .then(html => {
    container.innerHTML = html;
  })
  .catch(error => {
    console.error('Failed to fetch extension HTML:', error);
  });
