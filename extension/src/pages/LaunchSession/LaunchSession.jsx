import React, { useState } from 'react';
import logo from '../../assets/img/icon-500.png';
import './LaunchSession.css';
import './LaunchSession.scss';
import { AwesomeButton } from "react-awesome-button";
import AwesomeButtonStyles from "react-awesome-button/src/styles/styles.scss";
import io from 'socket.io-client';
import Debounce from '../../../utils/debounce';
import TextareaAutosize from 'react-textarea-autosize';

const OMEGALEARN_SESSION_ID_LOCAL_STORAGE_KEY = "omegalearnSessionID";
const OMEGALEARN_SESSION_URL_LOCAL_STORAGE_KEY = "omegalearnSessionUrl";

const getLocalStorageSessionId = () => {
  return localStorage.getItem(OMEGALEARN_SESSION_ID_LOCAL_STORAGE_KEY);
}  

const getLocalStorageSessionUrl = () => {
  return localStorage.getItem(OMEGALEARN_SESSION_URL_LOCAL_STORAGE_KEY);
}  

let socket = null;

if(socket == null){
    socket = io.connect("https://omegalearn.tech");
}

const LaunchSession = () => {
  const [localStorageSessionId, setLocalStorageSessionId] = useState(getLocalStorageSessionId());
  const [sessionNote, setSessionNote] = useState("");

  const emitUpdateNoteEvent = Debounce((value) => {
    socket.emit("note edited", {
      note: value,
      url:  getLocalStorageSessionUrl()
    });
  }, 250);

  const updateNote = (ev) => {
      emitUpdateNoteEvent(ev.target.value);
      setSessionNote(ev.target.value);
  }

  socket.on('note updated', (msg)=>{
      setSessionNote(msg.content)
  });

  const getSessionFoundJSX = () => {
    return (
      <div className="Launch-session">
        <div className = "Session-found">
            <div className="Session-title">
              <b>We've found a session!</b>
            </div>
            <AwesomeButton
              cssModule={AwesomeButtonStyles}
              type="secondary"
              ripple
              onPress={() => {
                localStorage.setItem(OMEGALEARN_SESSION_ID_LOCAL_STORAGE_KEY, "null");
                window.open("https://omegalearn.tech/call/"+localStorageSessionId, '_blank');
              }}
            >Join Session</AwesomeButton>
          </div>
          <div className="Launch-notes">
            <div className="Launch-notes-title">
                <b>Notes</b>
            </div>
           <TextareaAutosize cacheMeasurements value={sessionNote} minRows={4} onChange={updateNote}/>
        </div>
      </div>
     )
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {localStorageSessionId && localStorageSessionId!="null" && getSessionFoundJSX()}
        <h6>Happy chatting!</h6>
        <h5>Url: {getLocalStorageSessionUrl()}</h5>
      </header>
    </div>
  );
};

export default LaunchSession;
