var query = { active: true, currentWindow: true };
var dataTab = {url: "",title: ""}
var listData = []
function callback(tabs) {
    var currentTab = tabs[0]; // there will be only one in this array
    dataTab.url = currentTab.url;
    dataTab.title = currentTab.title;
    console.log(currentTab); // also has properties like currentTab.id
    $("#txtUrlTab").val(dataTab.url)
}
chrome.tabs.query(query, callback);

function onChangeListVideos(data){
    let html = "";
    $("#videosdl_content").empty();
    data.forEach((item,index) => {
        html += `<tr>
            <td>${index+1}</td>
            <td>${item.url}</td>
            <td>${item.title}</td>
            <td>${item.name}</td>
            <td>${item.asin}</td>
            <td>${item.detail}</td>
            <td><input type="button" id="${item._id}" value="Del"></td>
        </tr>`;
    });
    $("#videosdl_content").html(html);
}

function removeID(vid){
    $.ajax({url: `https://www.inotepad.cloud/delVideosdlJson`, data: {_id: vid},method: "POST", success: function(result){
        if(!result.error){
            chrome.storage.local.get(['keyID'], function(result) {
                update_data(result.keyID);
            });
        }
    }});
}
function updateEvent(listID){
    listID.forEach(item=>{
        document.getElementById(item).addEventListener("click", ()=>{
            removeID(item);
        });
    })
    
}
function updateDataArray(data){
    listData = [];
    data.forEach(element => {
        listData.push(element._id)
    });
    onChangeListVideos(data)
    updateEvent(listData)
}
async function auth_key(keyId){
    var key = keyId;
    var pass = false;
    await $.ajax({url: `https://www.inotepad.cloud/api_key_videosdl?key=${key}`, success: function(result){
        pass = !result.error;
        if(!result.error){
            $("#msg_key").html(`<div style="color: green">${result.message}</div>`);
            $("#manage_video").show();
        }else{
            $("#manage_video").hide();
            $("#msg_key").html(`<div style="color: red">${result.message}</div>`);

        }
    }});
    if(pass){
        update_data(key);
    }
    return pass;
}
function update_data(keyId){
	var key = keyId;
    $.ajax({url: `https://www.inotepad.cloud/queryVideosdl?key=${key}`, success: function(result){
        if(!result.error){
            updateDataArray(result.data)
        }
    }});
}
document.addEventListener('DOMContentLoaded', function() {
    var btnUpdate = document.getElementById('btnUpdate');
    var btnManage = document.getElementById('btnManage');
    var btnAddVideos = document.getElementById('btnAddVideos');
    var btnDelAllVideosdl = document.getElementById('btnDelAllVideosdl');
    // onClick's logic below:
    btnUpdate.addEventListener('click', function() {
        clUpdateKey();
    });
    btnManage.addEventListener('click', function() {
        var newURL = "https://www.inotepad.cloud/videosdl";
        chrome.tabs.create({ url: newURL });
    });
    btnDelAllVideosdl.addEventListener('click', function() {
        let listID = listData;
        let key = $("#keyID").val();
        $.ajax({url: `https://www.inotepad.cloud/delAllVideosDL`, data: {listID: listID},method: "POST", success: function(result){
            if(!result.error){
                $("#videosdl_content").empty();
                auth_key(key)
            }
        }});
    });
    btnAddVideos.addEventListener('click', function() {
        let url = $("#txtUrlTab").val();
        let asin = $("#txtAsin").val();
        let user_id = $("#keyID").val();
        let title = dataTab.title;
        let name = "", detail="";
        $.ajax({url: `https://www.inotepad.cloud/addVideosDLJson`, data: {user_id: user_id,url:url,asin: asin,title: title,name: name,detail: detail},method: "POST", success: function(result){
            console.log(result)
            if(!result.error){
                updateDataArray(result.data)
            }
        }});
    });
});



function clUpdateKey(){
    console.log("Click")
    let keyID = $("#keyID").val()
    chrome.storage.local.set({keyID: keyID}, function() {
        console.log('Value is set to ' + keyID);
    });
    auth_key(keyID)
}