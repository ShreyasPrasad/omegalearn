import React, { useState } from 'react';
import logo from '../../assets/img/icon-500.png';
import Switch from "react-switch";
import './Popup.css';

const OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY = "omegalearnAvailability";

const getLocalStorageAvailability = () => {
  return localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY);
}

const Popup = () => {

  const [localStorageAvailability, setLocalStorageAvailability] = useState(getLocalStorageAvailability());

  const handleAvailabilityChange = (evt) => {
    localStorage.setItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY, evt ? "true" : "false");
    setLocalStorageAvailability(localStorage.getItem(OMEGALEARN_AVAILABILITY_LOCAL_STORAGE_KEY));
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome to <b>Omegalearn!</b> Toggle your availability to find someone else interested in what you're browsing!
        </p>
        <Switch onChange={handleAvailabilityChange} checked={localStorageAvailability === "true"} />
      </header>
    </div>
  );
};

export default Popup;