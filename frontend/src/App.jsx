import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/ChatPage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import LeadsPage from './pages/LeadsPage.jsx';
import LeadDetailsPage from './pages/LeadDetailsPage.jsx';
import FollowUpsPage from './pages/FollowUpsPage.jsx';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/leads" element={<LeadsPage />} />
        <Route path="/leads/:id" element={<LeadDetailsPage />} />
        <Route path="/follow-ups" element={<FollowUpsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
