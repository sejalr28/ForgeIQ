import {
    Menu,
    LayoutDashboard,
    Cpu,
    Bot,
    TriangleAlert,
    Settings,
    Factory
} from "lucide-react";

const menu = [
    {
        icon: LayoutDashboard,
        label: "Dashboard"
    },
    {
        icon: Cpu,
        label: "Machines"
    },
    {
        icon: Bot,
        label: "AI Prediction"
    },
    {
        icon: TriangleAlert,
        label: "Alerts"
    }
];

function Sidebar(){

    return(

<div className="w-64 bg-white border-r border-slate-200 flex flex-col">

<div className="flex items-center justify-between px-6 py-6">

<div className="flex items-center gap-3">

<div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">

<Factory className="text-white" size={20}/>

</div>

<div>

<h2 className="font-bold text-lg">
ForgeIQ
</h2>

<p className="text-xs text-slate-500">
Manufacturing AI
</p>

</div>

</div>

<Menu className="text-slate-500 cursor-pointer"/>

</div>

<nav className="flex-1 mt-8 px-4">

{

menu.map((item)=>{

const Icon=item.icon;

return(

<div
key={item.label}
className="flex items-center gap-4 px-4 py-3 rounded-xl mb-2 cursor-pointer hover:bg-blue-50 hover:text-blue-600 transition">

<Icon size={20}/>

<span className="font-medium">

{item.label}

</span>

</div>

)

})

}

</nav>

<div className="p-4">

<div className="flex items-center gap-4 px-4 py-3 rounded-xl hover:bg-slate-100 cursor-pointer">

<Settings size={20}/>

<span>

Settings

</span>

</div>

</div>

</div>

)

}

export default Sidebar;