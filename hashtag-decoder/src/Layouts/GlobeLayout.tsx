import React, { useRef, useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import GeneralInformation from '../Components/GeneralInformation';
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Tooltip,
	Legend,
	ScriptableContext
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Tooltip,
	Legend
);

export const options = {
	responsive: true,
	maintainAspectRatio: false,
	elements: {
		point:{
			radius: [0,0,0,0,4]
		},
		line: {
			tension: 0.4,
		}
	},
    scales: {
        x: {
            grid: {
                display: false,
            },
            ticks: {
                display: false,
            },
        },
        y: {
            grid: {
                display: false,
            },
            ticks: {
                display: false,
            },
        },
    },
	plugins: {
		title: {
			display: false,
		},
		legend: {
			display: true,
			labels: {
				boxWidth: 2,
				color: '#7F7F7F',
				font: {
					size: 8,
				},
			},
			position: 'bottom' as const,
			align: 'center' as const,
		}
	},
};


const labels = [1, 2, 3, 4, 5];

export const data = {
	labels,
	datasets: [
		{	
			label: '30% Happy',
			data: labels.map(e => -Math.cos(e)),
			borderColor: '#4690FF',
			fill: false,
			backgroundColor: [
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(70, 144, 255, 1)',
			],
		},
		{
			label: '30% Bad',
			data: labels.map(e => Math.cos(e)),
			borderColor: '#F64BBC',
			fill: false,
			backgroundColor: [
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(246, 75, 188, 1)',
			],
		},
		{
			label: '40% Neutral',
			data: labels.map(e => Math.sin(e)),
			borderColor: '#3E03A1',
			fill: false,
			backgroundColor: [
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(0, 0, 0, 0.0)',
			  'rgba(62, 3, 161, 1)',
			],
		},
	],
};

const GlobeLayout: React.FC = () => {

	
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
			<GeneralInformation/>
			<div className="h-[6rem] pr-48 pl-24">
				<Line options={options} data={data}/>
			</div>
		</div>
	);
};

export default GlobeLayout;
