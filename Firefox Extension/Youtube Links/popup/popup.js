// a.ytcp-video-info
var listData = []

let m_date = new Date();
let day = (m_date.getDate() >= 10) ? m_date.getDate() : "0"+m_date.getDate();
let month = (m_date.getMonth()+1 >= 10) ? m_date.getMonth()+1 : "0"+(m_date.getMonth()+1);
var d_public = `${m_date.getFullYear()}-${month}-${day}`;

var t_public = ["T22:45","T23:00","T23:15","T23:30","T23:45","T12:00"];
var pos = 0;

function nextTime(){
    if(pos >= t_public.length-1){
        pos = 0;
    }else{
        pos++;
    }
    browser.storage.local.set({
        pos:  pos
    });
}

async function updateURL(){
    let urlCode = await browser.tabs.executeScript({
		code: `document.querySelector("a.ytcp-video-info").outerText;`
	});
    
    let channelCode = await browser.tabs.executeScript({
		code: `document.querySelector("#entity-name").outerText;`
	});
    let keywordCode = await browser.tabs.executeScript({
		code: `document.querySelector("#title-textarea > ytcp-form-input-container:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > ytcp-mention-input:nth-child(1) > div:nth-child(1)").outerText;`
	});
    
    $("#txtUrlTab").val(urlCode[0])
    $("#txtChannel").val(channelCode[0])
    $("#txtKeyword").val(keywordCode[0])
    console.log(keywordCode);
}
async function auth_key(keyId){
    var key = keyId;
    var pass = false;
    console.log("KEY",keyId)
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
        console.log("PASS",pass)
        update_data(key);
        updateURL();
    }
    return pass;
}
function onChangeListVideos(data){
    let html = "";
    $("#videosdl_content").empty();
    data.forEach((item,index) => {
        html += `<tr>
            <td>${index+1}</td>
            <td>${item.url}</td>
            <td>${item.public}</td>
        </tr>`;
    });
    $("#videosdl_content").html(html);
}

function updateDataArray(data){
    data.forEach(element => {
        listData.push(element._id)
    });
    onChangeListVideos(data)
}

function update_data(keyId){
	var key = keyId;
    $.ajax({url: `https://www.inotepad.cloud/queryVideo?watch=all&filter=day&auth=0`, success: function(result){
        console.log("UPDATE DATA")    
        if(result.data.length>0){
            updateDataArray(result.data)
        }
    }});
}

function clUpdateKey(){
    console.log("Click")
    let keyID = $("#keyID").val()
    browser.storage.local.set({
        keyID:  keyID
    });
    auth_key(keyID)
}
function clearTimer(){
    pos = 0;
    browser.storage.local.set({
        pos:  0
    });
    $("#txtTimer").val(d_public+t_public[pos]);
}

function btnAddVideos(){
    let keyID = ""
    let channel = $("#txtChannel").val();
    let keyword = $("#txtKeyword").val();
    let public = $("#txtTimer").val();
    let url = $("#txtUrlTab").val();
    let data = {
        keyID: keyID,
        channel: channel,
        keyword: keyword,
        public: public,
        url: url,
        success: false
    }
    let itemKey = browser.storage.local.get("keyID");
    itemKey.then(item=>{
        keyID = item.keyID;
        data.keyID = keyID;
        $.ajax({
            url : "https://www.inotepad.cloud/addVideoPost",
            data : data, //key: value
            method : 'post',
            dataType: 'json',
            success: function(data){
                if(!data.error){
                    nextTime()
                    $("#txtTimer").val(d_public+t_public[pos]);
                    update_data(keyID)
                }
                
            }
            ,
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            } 
        });
    });
    
    
}

document.addEventListener('DOMContentLoaded', function() {
    var btnUpdate = document.getElementById('btnUpdate');
    var btnVideos = document.getElementById('btnVideos');
    var btnManage = document.getElementById('btnManage');
    var btnResetTimer = document.getElementById('btnResetTimer');

    // onClick's logic below:
    btnUpdate.addEventListener('click', function() {
        clUpdateKey();
    });
    btnVideos.addEventListener('click', function() {
        btnAddVideos();
    });
    btnManage.addEventListener('click', function() {
        var newURL = "https://www.inotepad.cloud/listVideos";
        chrome.tabs.create({ url: newURL });
    });
    btnResetTimer.addEventListener('click', function() {
        clearTimer();
    });
});
$(document).ready(async ()=>{
    
    let itemKey = browser.storage.local.get("keyID");
    let posLocal = browser.storage.local.get("pos");
    itemKey.then(item=>{
        $("#keyID").val(item.keyID);
        auth_key(item.keyID)
    });
    posLocal.then(item=>{
        if(item.pos != undefined){
            pos = item.pos;
        }else{
            pos = 0;
        }
        $("#txtTimer").val(d_public+t_public[pos]);
    });

})