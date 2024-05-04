import {Router} from '@vaadin/router';
import './components/home.ts';
import './components/about.ts';

window.addEventListener('load', () => {
    const outlet = document.querySelector('#outlet');
    const router = new Router(outlet);

    // noinspection JSIgnoredPromiseFromCall
    router.setRoutes([
        {path: '/', component: 'main-page'},
        {path: '/about', component: 'about-page'}
    ]);
});
