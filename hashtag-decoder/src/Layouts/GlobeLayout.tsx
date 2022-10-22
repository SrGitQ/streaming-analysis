import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import GeneralInformation from '../Components/GeneralInformation';

const GlobeLayout: React.FC = () => {
	const data = [
		{"name":"Workout", "data": {"2021-01-01": 3, "2021-01-02": 4}},
		{"name":"Call parents", "data": {"2021-01-01": 5, "2021-01-02": 3}}
	];

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
			<div className="h-1/3">
				{/* <Line data={data}/> */}
			</div>
		</div>
	);
};

export default GlobeLayout;
