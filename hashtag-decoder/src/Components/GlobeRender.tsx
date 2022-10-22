import Globe from 'react-globe.gl';
import React, { useRef, useEffect } from "react";

const WorldR: React.FC = () => {
    const globeEl = useRef();

    useEffect(() => {
		// Auto-rotate
		if (globeEl.current) {
			const r = globeEl.current as any;
			if (r.controls) {
				r.controls().autoRotate = true;
				r.controls().autoRotateSpeed = 2;
			}
		}
	  }, []);

	return (
		<Globe
			ref={globeEl}
			backgroundColor='rgba(0, 0, 0, 0)'
			globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
			animateIn={true}
			pointsData={[
				{ lat: 21.009293505988, lng: -89.69595640433737},
			]}
			pointColor={() => '#219bf0'}
		/>
	);
};

const GlobeRender: React.FC = () => {
	
	return (
		<div className="flex justify-center pb-16">
			<WorldR/>
		</div>
	);
};

export default GlobeRender;
