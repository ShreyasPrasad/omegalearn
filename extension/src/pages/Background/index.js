import '../../assets/img/icon-34.png';
import '../../assets/img/icon-128.png';
import { io } from './socket.js';

const tabIdMap = {};
let socket;
const OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY = "omegalearnAvailability";
const OMEGALEARN_CHROME_ID_LOCAL_STORAGE_KEY = "chrome_id";

//generate unique chrome_id when chrome extension is loaded
const getRandomToken = () => {
    // E.g. 8 * 32 = 256 bits token
    var randomPool = new Uint8Array(8);
    crypto.getRandomValues(randomPool);
    var hex = '';
    for (var i = 0; i < randomPool.length; ++i) {
        hex += randomPool[i].toString(16);
    }
    // E.g. db18458e2782b2b77e36769c569e263a53885a9944dd0a861e5064eac16f1a
    return hex;
}

chrome.runtime.onInstalled.addListener(function(details){
    const generated_chrome_id = getRandomToken();
    localStorage.setItem(OMEGALEARN_CHROME_ID_LOCAL_STORAGE_KEY, generated_chrome_id);
    socket = io.connect('https://omegalearn.tech');
});

socket.on('connect', function () {
    console.log("connected to omegalearn.tech");
    socket.emit('my event', {
      data: 'User Connected'
    })
});

socket.on('my response', function (msg) {
    console.log( msg )
});


chrome.tabs.onUpdated.addListener(function(tabId, info, tab) {
    if(tab.url!="chrome://newtab/" && localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY) == "true"){
        //send event to backend signalling new tab creation with non-trivial URL
        const formattedURL = tab.url.replace(/(^\w+:|^)\/\//, '');
        socket.emit('url added', {
            url: formattedURL,
            chrome_id: localStorage.getItem(OMEGALEARN_CHROME_ID_LOCAL_STORAGE_KEY)
        });
        tabIdMap[tabId]=formattedURL;
    }
});

chrome.tabs.onRemoved.addListener(function(tabId, removed) {
    if(localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY) == "true" && tabIdMap[tabId]){
        //send event to backend signalling removal of non-trivial URL
        socket.emit('url removed', {
            url: tabIdMap[tabId],
            chrome_id: localStorage.getItem(OMEGALEARN_CHROME_ID_LOCAL_STORAGE_KEY)
        });
        delete tabIdMap[tabId];
    }
});