chrome.tabs.onUpdated.addListener(function(tabId, info, tab) {
   if (info.status === 'complete') {
       console.log("TEST")
	   window.location.href = "https://google.com"
   }
});