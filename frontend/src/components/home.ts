import {LitElement, html, css} from 'lit';
import {SlChangeEvent, SlInput} from "@shoelace-style/shoelace";

class Home extends LitElement {

    static styles = css`
      :host {
        display: block;
        padding: 16px;
        text-align: center;
      }

      h1 {
        color: black;
      }

      .form-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        margin: 20px;
      }

      sl-input {
        flex: 1 1 auto;
        max-width: 300px;
      }

      sl-button {
        flex: 0 1 auto;
      }
    `;

    private name: string = '';

    fetchData() {
        const url = this.name ? `/api/test?name=${encodeURIComponent(this.name)}` : '/api/test';
        console.log(`Fetching ${url}`);
        fetch(url)
            .then(response => response.text())
            .then(data => {
                console.log(data);
                this.shadowRoot!.querySelector('h1')!.innerHTML = data;
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    render() {
        return html`
            <nav-bar></nav-bar>
            <h1>Hello, World!</h1>
            <div class="form-container">
                <sl-input placeholder="Enter your name"
                          @sl-change="${(e: SlChangeEvent) => this.name = (e.target as SlInput).value}"></sl-input>
                <sl-button @click="${this.fetchData}">Click me!</sl-button>
            </div>
        `;
    }
}

customElements.define('main-page', Home);
