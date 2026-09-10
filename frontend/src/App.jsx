import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/ChatPage.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        {/* Future routes:
            /dashboard
            /leads
            /leads/:id
            /follow-ups
        */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
