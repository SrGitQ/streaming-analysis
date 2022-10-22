import React, { useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import Bullet from '../Components/Bullet';
import { Graph, useNode, useLink } from 'graphire'

const Link = (props:{ source:number|string, target:number|string }) => {
	const color = 'gray'
	const rest = props
	const ref = useRef()
  
	useLink(([x1, y1], [x2, y2]) => {
		// @ts-ignore
	  	ref.current.setAttribute('x1', x1)  
	  	// @ts-ignore
	  	ref.current.setAttribute('y1', y1)  
	  	// @ts-ignore
	  	ref.current.setAttribute('x2', x2)  
	  	// @ts-ignore
	  	ref.current.setAttribute('y2', y2)  
	}, rest.source, rest.target)
	return (
		// @ts-ignore
	  	<line ref={ref} x1='0' y1='0' x2='0' y2='0' stroke={color} strokeWidth={1} />
	)
  }


// @ts-ignore-all
const Node = (props: { uid:number|string, x:number, y:number}) => {
	const color = '#FB71F2'
	const radius = 5
	const rest = props
	const ref = useRef()
	useNode(([cx, cy]) => {
		// @ts-ignore
		ref.current.setAttribute('cx', cx)
		// @ts-ignore
		ref.current.setAttribute('cy', cy)
	}, rest) 
	// @ts-ignore
	return <circle ref={ref} cx='0' cy='0' r={radius} fill={color} />
}

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
			<div className='h-full'>
    			<svg className='w-full h-full'>
    			  <Graph dim={3}>
        			<Node uid={0} x={110} y={100}	/>
        			<Node uid={1} x={50}  y={30}	/>
        			<Node uid={2} x={150} y={80}	/>
        			<Node uid='k' x={100} y={200}	/>
        			<Node uid={3} x={200} y={100}	/>

    			    <Link source={0} target={1} />
    			    <Link source={1} target={2} />
    			    <Link source={1} target='k' />
    			    <Link source={3} target='k' />
    			  </Graph>
    			</svg>

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
