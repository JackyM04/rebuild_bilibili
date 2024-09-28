import Image from 'next/image';
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
const VideoCard = ({ videoitem }: { videoitem: Videoitem }) => {
    return (
        <div className={`relative flex w-[240px] h-[170px] bg-slate-100 p-1 felx flex-col z-0 drop-shadow-md rounded-xl`} >
            <Image src={videoitem.pic} className="relative rounded-xl overflow-clip w-[240px] h-[135px] z-0" alt="video" width={672} height={378} layout="fixed"/>
            <div className='relative flex w-full h-10 bg-gradient-to-t from-black to-transparent rounded-b-xl z-10 mt-[-40px] place-content-end p-2'>
                <p className="text-white text-sm truncate place-self-end">{`${(videoitem.duration/60)|0}:${(videoitem.duration%60)}`}</p>
            </div>
            <p className="w-full text-base text-gray-950 truncate mx-3 drop-shadow-md">{videoitem.title}</p>
        </div>
    );
    };
export default VideoCard;