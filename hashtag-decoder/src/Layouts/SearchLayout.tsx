import React from 'react';

const SearchLayout:React.FC = () => {
	const [search, setSearch] = React.useState<string>("#");

	return (
		<div className="flex justify-center h-full">
			<div className="grid content-center">
				<form>
					<h1 className="text-white text-7xl text-center">
						<input 
							type="text" 
							name="name" 
							style={{all:'unset', caretColor: 'transparent'}}
							value={search}
							onChange={search => setSearch('#'+search.target.value.replace(/(#|\s|[<>\-_\.`^\[\]\{\}ç¨´:,;=\(\)\/&%$·"!\+\*\?\¡\¿Ç…„–œæ€®†¥  øπå∫∂ƒ™¶§ ~Ω∑©√ß µñÑ≠”“÷¬∞¢#@\|≤s≥\\ºª‚])/g,''))}
						/>
					</h1>
				</form>
			</div>
		</div>
	);
};

export default SearchLayout;
