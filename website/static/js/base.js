document.addEventListener('DOMContentLoaded', function() {
  const searchBox = document.querySelector('#search input[name="keyword"]');
  const searchResults = document.querySelector('#search .search-popup');
  const searchPopupItems = searchResults.querySelectorAll('.search-popup .items a');
  let selectedItemIndex = -1;

  // Add event listeners to the search box
  searchBox.addEventListener('focus', function() {
    // Show the search results div
    searchResults.style.display = 'block';
  });

  searchBox.addEventListener('blur', function() {
    // Hide the search results div after a short delay
    setTimeout(function() {
      searchResults.style.display = 'none';
    }, 200);
  });

  // Add event listeners to handle keyboard navigation
  document.addEventListener('keydown', function(event) {
    if (event.key === 's') {
      // Show the search box
      searchBox.focus();
      event.preventDefault();
    } else if (event.key === 'ArrowUp') {
      // Move the selection up
      if (selectedItemIndex > 0) {
        selectedItemIndex--;
        updateSelection();
        event.preventDefault();
      }
    } else if (event.key === 'ArrowDown') {
      // Move the selection down
      if (selectedItemIndex < searchPopupItems.length - 1) {
        selectedItemIndex++;
        updateSelection();
        event.preventDefault();
      }
    } else if (event.key === 'Enter' && selectedItemIndex != -1) {
      // Follow the link of the selected item
      const selectedLink = searchPopupItems[selectedItemIndex].getAttribute('href');
      window.location.href = selectedLink;
      event.preventDefault();

    } else if (event.key === 'Escape') {
      // Hide the search box
      searchBox.blur();
      event.preventDefault();
    }
  });
  

  // Prevent the search results div from closing when clicked on
  searchResults.addEventListener('mousedown', function(event) {
    event.preventDefault();
  });

  function updateSelection() {
    for (let i = 0; i < searchPopupItems.length; i++) {
      if (i === selectedItemIndex) {
        searchPopupItems[i].classList.add('selected');
        searchPopupItems[i].style.backgroundColor = '#791cfb21';
      } else {
        searchPopupItems[i].classList.remove('selected');
        searchPopupItems[i].style.backgroundColor = 'transparent';
      }
    }
  }

});




///////////////////////////////////////////////////////////////////////////////


// Add event listener to the "Clear" button in the search results div
const clearButton = document.querySelector('.s-close');
clearButton.addEventListener('click', function() {
  // Clear the search box and hide the search results div
  searchBox.value = '';
  searchResults.style.display = 'none';
});

// NAVBAR PROFILE AVATAR ONLICK DROP MENU ITEMS
const avatar = document.querySelector('.avatar');
const dropdownMenu = document.querySelector('.dropdown-menu');

avatar.addEventListener('click', function() {
  dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('click', function(event) {
  if (!avatar.contains(event.target) && !dropdownMenu.contains(event.target)) {
    dropdownMenu.style.display = 'none';
  }
});