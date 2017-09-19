import React from 'react';
import { Route, IndexRoute } from 'react-router';
import App from './components/App';
import HomePage from './components/home/HomePage';
import PodsPage from './components/pods/PodsPage';
import PodPage from './components/pods/PodPage';
import PackPage from './components/packs/PackPage';

export default (
  <Route path="/" component={App}>
    <IndexRoute component={HomePage} />
    <Route path="/pods" component={PodsPage} >
      <Route path="/pods/:id" component={PodPage} />
    </Route>
    <Route path="/pods/:podId/recap" component={PodPage} />
    <Route path="/players/:email/pods" component={PodsPage} />
    <Route path="/players/:hash/pack" component={PackPage} />
  </Route>
);
