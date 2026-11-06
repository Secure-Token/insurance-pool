import React from 'react';
import {Routes,Route,Navigate} from 'react-router-dom';
import Layout from './layouts/Layout.jsx';
import Dashboard from './pages/Dashboard.jsx';
import ClaimSubmission from './pages/ClaimSubmission.jsx';
import Claims from './pages/Claims.jsx';
import ClaimDetail from './pages/ClaimDetail.jsx';
import Investigations from './pages/Investigations.jsx';
import Pool from './pages/Pool.jsx';
import Ledger from './pages/Ledger.jsx';
export default function App(){return <Routes><Route element={<Layout/>}><Route index element={<Dashboard/>}/><Route path="claim/new" element={<ClaimSubmission/>}/><Route path="claims" element={<Claims/>}/><Route path="claims/:id" element={<ClaimDetail/>}/><Route path="investigations" element={<Investigations/>}/><Route path="pool" element={<Pool/>}/><Route path="ledger" element={<Ledger/>}/><Route path="*" element={<Navigate to="/" replace/>}/></Route></Routes>}