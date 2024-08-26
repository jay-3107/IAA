import { Link } from 'react-router-dom';


const Hero = () => {
  return (
    <section id="hero">
      {/* Flex Container */}
      <div className="container flex flex-col-reverse items-center px-6 mx-auto mt-10 space-y-0 md:space-y-0 md:flex-row">
        {/* Left Item */}
        <div className="flex flex-col mb-32 space-y-12 md:w-1/2">
          <h1 className="max-w-md text-4xl font-bold text-center md:text-5xl md:text-left">
          Indian Aviation Academy
          Nurturing Aviation for the Future
          </h1>
          <p className="max-w-sm text-center text-darkGrayishBlue md:text-left">
          Indian Aviation Academy (IAA), is the joint training academy of the Airports Authority of India (AAI), Director General of Civil Aviation (DGCA) and Bureau of Civil Aviation Security (BCAS). Its history can be traced back to year 1986, when the Institute of Airport Management started its operations from Patterson Farm House, located near Indira Gandhi International Airport. The Institute moved to its present campus in 1988. The new building was inaugurated by the Secretary General, ICAO in December, 1988. It was renamed as National Institute of Aviation Management and Research (NIAMAR) in 1997. In 2010, NIAMAR was transformed into the Indian Aviation Academy. 
          </p>
          <div className="flex justify-center md:justify-start">
            <Link
              to="#"
              className="p-3 px-6 pt-2 text-white bg-[#22409A] rounded-full baseline hover:bg-brightRedLight"
            >
              Get Started
            </Link>
          </div>
        </div>
        {/* Image */}
        <div className="md:w-1/2 ">
          <img src="../src/assets/images/airplane-image.png" alt="image" />
        </div>
      </div>
    </section>
  );
};

export default Hero;
