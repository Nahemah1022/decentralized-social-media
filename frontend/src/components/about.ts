import { LitElement, html, css } from 'lit';
import './nav.ts';

class About extends LitElement {
    static styles = css`
      :host {
        display: block;
        padding: 16px;
        text-align: center;
      }

      h1 {
        color: black;
      }
    `;

    render() {
        return html`
            <nav-bar></nav-bar>
            <h1>About</h1>
        `;
    }
}

customElements.define('about-page', About);
