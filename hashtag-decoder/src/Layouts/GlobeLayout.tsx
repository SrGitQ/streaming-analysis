import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import GeneralInformation from '../Components/GeneralInformation';
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Tooltip,
);

export const options = {
	responsive: true,
	maintainAspectRatio: false,
	elements: {
		point:{
			radius: 0
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

	},
};


const labels = [1, 2, 3, 4, 5];

export const data = {
	labels,
	datasets: [
		{	
			label: 'Dataset 1',
			data: labels.map(e => Math.cos(e)),
			borderColor: '#4690FF',
		},
		{
			label: 'Dataset 2',
			data: labels.map(e => -Math.cos(e)),
			borderColor: '#F64BBC',
		},
		{
			label: 'Dataset 3',
			data: labels.map(e => Math.sin(e)),
			borderColor: '#3E03A1',
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
			<div className="h-[4rem] pr-48 pl-24">+
			</div>
		</div>
	);
};

export default GlobeLayout;
