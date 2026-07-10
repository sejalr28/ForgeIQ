import {

Bell,

Search,

CircleUser

} from "lucide-react";

function Header(){

return(

<header className="bg-white border-b border-slate-200 h-20 px-10 flex justify-between items-center">

<div>

<h1 className="text-3xl font-bold">

Dashboard

</h1>

<p className="text-slate-500">

Manufacturing Overview

</p>

</div>

<div className="flex items-center gap-5">

<div className="flex items-center gap-3 bg-slate-100 rounded-xl px-4 py-3">

<Search
size={18}
className="text-slate-500"/>

<input
placeholder="Search machines..."
className="bg-transparent outline-none w-60"/>

</div>

<Bell
className="cursor-pointer"/>

<CircleUser
size={34}
className="cursor-pointer"/>

</div>

</header>

)

}

export default Header;