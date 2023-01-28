import { Route, Routes } from 'react-router-dom';
import Login from './Pages/Login';
import DashboardX from './Pages/Dashboard';
import Question from './Components/Question';
import Help from './Components/Help';
import Home from './Components/Home';
import ScoreBoardX from './Components/Scoreboard';
import ProfileX from './Components/Profile';
import Questions from './Pages/Questions';
import "./App.css";
import { UserContextProvider } from './Store/user';
function App() {
  return (
    <div>
      <UserContextProvider>
        <Routes>
          <Route path='login' element={<Login />}></Route>
          <Route path="s" element={<DashboardX />}>
            <Route path="dashboard" element={<Home />}></Route>
            <Route path="help" element={<Help />}></Route>
            <Route path="scoreboard" element={<ScoreBoardX />}></Route>
            <Route path="profile" element={<ProfileX />}></Route>
          </Route>
          <Route path="q" element={<Questions />}>
            <Route path="" element={<Question />}></Route>
          </Route>
          {/* <Route path="question" element = {<Question/>}></Route> */}
        </Routes>
      </UserContextProvider>
    </div>
  );
}

export default App;
