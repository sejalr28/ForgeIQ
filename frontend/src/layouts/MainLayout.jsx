import Sidebar from "../components/Sidebar";
import Header from "../components/Header";

function MainLayout({children}){

return(

<div className="flex h-screen bg-slate-50">

<Sidebar/>

<div className="flex-1 flex flex-col">

<Header/>

<main className="flex-1 p-8 overflow-auto">

{children}

</main>

</div>

</div>

)

}

export default MainLayout;