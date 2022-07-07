var key_id = "";
$(document).ready(()=>{
	chrome.storage.local.get(['keyID'], function(result) {
		console.log('Value currently is ' + result.keyID);
		$("#keyID").val(result.keyID);
		let key_id = result.keyID;
		auth_key(key_id);
	});
	
})
