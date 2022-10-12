require("dotenv").config({ path: "./db/database.env" });
const db = require("./connection.js");

//seed can be run from "make setup-env" from oapen-engine/
//"7b5fdf5b-9ffa-4073-84fe-c21cce0025b5"	"Energy Poverty, Practice, and Policy"	"{""(7b5fdf5b-9ffa-4073-84fe-c21cce0025b5,0)""}"
//"a91a6b7d-874a-4144-b44d-0da647a82acc"	"The Future European Energy System"	"{""(a91a6b7d-874a-4144-b44d-0da647a82acc,1)""}"
//"858df59f-0014-4355-8435-dca9c187ce0c"	"Literatura latinoamericana mundial"	"{""(858df59f-0014-4355-8435-dca9c187ce0c,2)""}"
//"44c40c47-df67-476a-9603-3054f726b156"	"Religion and Governance in England’s Emerging Colonial Empire, 1601–1698"	"{""(44c40c47-df67-476a-9603-3054f726b156,3)""}"
//"2ce07264-58ac-426a-9c88-500f8b47e7f5"	"Open Science: the Very Idea"	"{""(2ce07264-58ac-426a-9c88-500f8b47e7f5,4)""}"
//"4ba6ae5d-1797-4def-b0d7-1cd8652e5cd9"	"Embodying Contagion"	"{""(4ba6ae5d-1797-4def-b0d7-1cd8652e5cd9,5)""}"
//"57753423-cb8a-4f08-815d-ac7aa19b049b"	"Thou Shalt Forget"	"{""(57753423-cb8a-4f08-815d-ac7aa19b049b,6)""}"
//"7df13adb-771b-4d66-b081-2345059622bc"	"Engines of Order"	"{""(7df13adb-771b-4d66-b081-2345059622bc,7)""}"
//"ae797d93-6c5e-46ee-a193-45cd7c114e65"	"Atlas"	"{""(ae797d93-6c5e-46ee-a193-45cd7c114e65,8)""}"
//"8e001ebf-5e63-44f5-9f31-5d79389e0f14"	"Vulnerable"	"{""(8e001ebf-5e63-44f5-9f31-5d79389e0f14,9)""}"
