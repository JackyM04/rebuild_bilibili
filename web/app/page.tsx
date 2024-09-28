"use client"
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect, useRef } from "react";
import { useState } from "react";
import Cookies from 'js-cookie';
import VideoCard from "./video_card";
import { env } from "process";

export default function Home() {
  const recomveriourl = process.env.NEXT_PUBLIC_HOST_RECOMVIDEO;
  const backendHost = process.env.NEXT_PUBLIC_HOST_HTTP;
  const [videoList, setVideoList] = useState<Videoitem[]>([]);
  const [hasFetched, setHasFetched] = useState(false);
  const [isFocusedlogin, setIsFocusedlogin] = useState(false);

  const handleFocus = () => {
    setIsFocusedlogin(true);
  };

  const handleBlur = () => {
    setIsFocusedlogin(false);
  };

  type Videoitem = {
    uri: string;
    pic: string;
    title: string;
    duration: number;
    owner: {
      name: string;
      face: string;
    };
  }


  useEffect(() => {
      getvideoList();
    
  }, []);

  const getvideoList = async () => {
    if (!recomveriourl) {
      console.error("recomveriourl is not set");
      return;
    }
    fetch(`${backendHost}/api/get/recomvideo`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `${Cookies.get("token")||""}`
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.data.item);
        setVideoList(data.data.item);
    })
  };
  


  return (
    <main className="relative flex flex-col h-dvh w-screen text-black p-4 gap-4">
      <div className="relative flex flex-row h-14 w-full bg-blue-400 rounded-full drop p-1">
        <div className="flex-1 flex items-center">
          <span className="ml-4 text-white">这里放其他内容</span>
        </div>
        

        <Image src="https://i0.hdslb.com/bfs/face/3eff7bd25ecd0a4ed4a64a5b8de996d1146ef62e.jpg" 
        className="relative h-12 w-12 rounded-full place-self-center mr-0" alt="avatar" width={200} height={200} />
        <div onMouseEnter={handleFocus} onMouseLeave={handleBlur} className="">
          {isFocusedlogin ? (
            
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="size-12">
              <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25ZM12.75 9a.75.75 0 0 0-1.5 0v2.25H9a.75.75 0 0 0 0 1.5h2.25V15a.75.75 0 0 0 1.5 0v-2.25H15a.75.75 0 0 0 0-1.5h-2.25V9Z" clip-rule="evenodd" />
            </svg>
          ):(
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-12">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
            </svg>
          )}
        </div>

      </div>
      <div className="relative h-full w-full rounded-xl p-4 gap-4 bg-blue-300 flex flex-wrap overflow-scroll hide-scrollbar place-content-around">
        {videoList.map((video, index) => (<VideoCard key={index} videoitem={video}/>))}
      </div>
    </main>
  );
}
