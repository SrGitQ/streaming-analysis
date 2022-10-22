import React, { useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import Bullet from '../Components/Bullet';
import { ForceGraph3D } from 'react-force-graph';

const GraphLayout:React.FC = () => {
	return (
		<div className="h-full flex flex-col">
			<div className="h-[1.5rem] text-[#172158] text-center text-xl font-[1200]">
				<FontAwesomeIcon icon={solid('chevron-up')} />
			</div>
			<div className="h-1/6">
				<h1 className="text-white text-4xl font-bold">
					#AMLO
				</h1>
			</div>
			<div className='h-full flex justify-center pt-10'>
				<ForceGraph3D
					graphData={{
						nodes: [
							{ id: 'Harry' },
							{ id: 'Sally' },
							{ id: 'Alice' }
						],
						links: [
							{ source: 'Harry', target: 'Sally' },
							{ source: 'Harry', target: 'Alice' }
						]
					}}
					nodeLabel='id'
					nodeColor={() => '#FB71F2'}
					linkWidth={1}
					onNodeDragEnd={node => {
						node.fx = node.x;
						node.fy = node.y;
						node.fz = node.z;
					}
				}
				width={900}
				height={400}
				backgroundColor='rgba(0,0,0,0)'
				/>
			</div>
			<div className='h-28 flex justify-between pl-28 pr-28'>
				<Bullet title={'Tweets'} text={'4M'}/>
				<Bullet title={'Users'} text={'2.4K'}/>
				<Bullet title={'Hashtags'} text={'300'}/>
			</div>
		</div>
	);
};

export default GraphLayout;
