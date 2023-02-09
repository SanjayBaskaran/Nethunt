import { Outlet, Route, Routes } from 'react-router-dom';
import Login from './Pages/Login';
import DashboardX from './Pages/Dashboard';
import Question from './Components/Question';
import Help from './Components/Help';
import Home from './Components/Home';
import ScoreBoardX from './Components/Scoreboard';
import ProfileX from './Components/Profile';
import Questions from './Pages/Questions';
import "./App.css";
import { userContext, UserContextProvider } from './Store/user';
import AdminMain from './Pages/Admin/AdminMain';
import AdminHome from './Components/AdminHome';
import College from './Pages/Admin/College';
import Candidate from './Pages/Admin/Candidate';
import QuizSettings from './Pages/Admin/QuizSettings';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import CoordinatorsAdmin from './Pages/Admin/CoordinatorsAdmin';
import QuizDisplay from './Components/QuizDisplay';
import QuizEdit from './Components/QuizEdit';
import QuestionAdmin from './Components/QuestionsAdmin';

import { useContext } from 'react';
import jwtDecode from 'jwt-decode';
import Page404 from './Pages/404';
function App() {
  const { token } = useContext(userContext)
  return (
    <div>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
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
          
          {(token!=null&&jwtDecode(token?.access).role =="Admin")&&(<Route path="a" element={<AdminMain />} >
            <Route path="" element={<AdminHome />}></Route>
            <Route path="college" element={<College />}></Route>
            <Route path="qsettings" element={<QuizSettings />}></Route>
            <Route path="usr" element={<Candidate />}></Route>
            <Route path="crd" element={<CoordinatorsAdmin />}></Route>
            <Route path="quiz" element={<Outlet />}>
              <Route path="v" element={<QuizDisplay />}></Route>
              <Route path="e" element={<QuizEdit />}></Route>
              <Route path="q" element={<QuestionAdmin />}></Route>
            </Route>
            <Route path="score" element={<ScoreBoardX />}></Route>
          </Route>)}

          <Route path='*' element={<Page404/>}/>
          {/* <Route path="question" element = {<Question/>}></Route> */}
        </Routes>
      </LocalizationProvider>
    </div>
  );
}

export default App;
