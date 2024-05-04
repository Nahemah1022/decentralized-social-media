import { LitElement, html, css } from 'lit';

class NavBar extends LitElement {
    static styles = css`
      nav {
        text-align: center;
        margin-bottom: 20px;
      }

      a {
        padding: 8px;
        text-decoration: none;
        color: blue;
        font-size: 18px;
      }
    `;

    render() {
        return html`
            <nav>
                <a href="/">Home</a>
                <a href="/about">About</a>
            </nav>
        `;
    }
}

customElements.define('nav-bar', NavBar);
