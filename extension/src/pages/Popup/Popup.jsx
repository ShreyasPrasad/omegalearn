import React, { useState } from 'react';
import logo from '../../assets/img/logo.svg';
import Switch from "react-switch";
import './Popup.css';

const OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY = "omegalearnAvailability";

const getLocalStorageAvailability = () => {
  return localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY);
}

const Popup = () => {

  const [localStorageAvailability, setLocalStorageAvailability] = useState(getLocalStorageAvailability());
  const handleChange = (evt) => {
    localStorage.setItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY, evt ? "true" : "false");
    setLocalStorageAvailability(localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY));
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome to Omegalearn! Toggle your availability to find someone else interested in what you're browsing!
        </p>
        <Switch onChange={handleChange} checked={localStorageAvailability === "true"} />
      </header>
    </div>
  );
};

export default Popup;


/*

 <a
          className="App-link"
          href="newtab.html"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>

*/