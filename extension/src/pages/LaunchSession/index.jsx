import React from 'react';
import { render } from 'react-dom';

import LaunchSession from './LaunchSession';
import './index.css';

render(<LaunchSession />, window.document.querySelector('#app-container'));
