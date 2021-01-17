import React, { useState } from 'react';
import logo from '../../assets/img/icon-500.png';
import './LaunchSession.css';
import './LaunchSession.scss';
import { AwesomeButton } from "react-awesome-button";
import AwesomeButtonStyles from "react-awesome-button/src/styles/styles.scss";

const OMEGALEARN_SESSION_ID_LOCAL_STORAGE_KEY = "omegalearnSessionID";
const OMEGALEARN_SESSION_URL_LOCAL_STORAGE_KEY = "omegalearnSessionUrl";

const getLocalStorageSessionId = () => {
  return localStorage.getItem(OMEGALEARN_SESSION_ID_LOCAL_STORAGE_KEY);
}  

const getLocalStorageSessionUrl = () => {
  return localStorage.getItem(OMEGALEARN_SESSION_URL_LOCAL_STORAGE_KEY);
}  

const LaunchSession = () => {
  const [localStorageSessionId, setLocalStorageSessionId] = useState(getLocalStorageSessionId());
  const getSessionFoundJSX = () => {
    return (
    <div className = "Session-found">
        <div>
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
      </div>)
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {localStorageSessionId && localStorageSessionId!="null" && getSessionFoundJSX()}
        <h6>Happy chatting!</h6>
        <h5>Topic: {getLocalStorageSessionUrl()}</h5>
      </header>
    </div>
  );
};

export default LaunchSession;
