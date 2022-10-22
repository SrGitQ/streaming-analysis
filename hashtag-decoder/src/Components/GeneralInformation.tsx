import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro';
import Bullet from './Bullet';

const GeneralInformation: React.FC = () => {
	return (
		<div className="h-2/3 flex ">
			<div className="w-1/5 flex flex-col space-y-8">
				<Bullet title="Tweets" text="4M"/>
				<Bullet title="Users" text="2.3K"/>
				<Bullet title="Mentions" text="300"/>
			</div>
			<div className="w-full">
				
			</div>
			<div className="w-1/5 flex flex-col space-y-8">
				<Bullet title="Places" text="24"/>
				<div className="w-18 flex flex-col m-auto">
					<div className="text-white flex justify-between w-[4rem]">
						<FontAwesomeIcon icon={solid('laptop')} />
						<div>304</div>
					</div>
					<div className="text-white flex justify-between w-[4rem]">
						<FontAwesomeIcon icon={solid('apple-whole')} />
						<div>304</div>
					</div>
					<div className="text-white flex justify-between w-[4rem]">
						<FontAwesomeIcon icon={solid('mobile')} />
						<div>304</div>
					</div>
				</div>
				<Bullet title="Verified Users" text="1K"/>
			</div>
		</div>
	);
};

export default GeneralInformation;
