// Create a button in the extension's user interface
const button = document.createElement('button');
button.textContent = 'Authenticate with Graphical Password';
document.body.appendChild(button);

// Add an event listener to the button
button.addEventListener('click', () => {
  // Create a new tab with the graphical password interface
  chrome.tabs.update({ url: 'templates/index.html' }, (tab) => {
    // Send a message to the background page with the tab ID
    chrome.runtime.sendMessage({ tabId: tab.id });
  });
});

