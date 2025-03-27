import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Client as Styletron } from 'styletron-engine-monolithic';
import { Provider as StyletronProvider } from 'styletron-react';
import { LightTheme, BaseProvider } from 'baseui';
import App from './App.tsx'

const engine = new Styletron();
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>

        <App />
      </BaseProvider>
    </StyletronProvider>
  </StrictMode>,
)
