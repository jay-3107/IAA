import { Link } from 'react-router-dom';


const Hero = () => {
  return (
    <section className='flex justify-center' id="hero">
      {/* Flex Container */}
      <div className="container flex flex-col-reverse items-center px-6 mx-auto mt-10 ml-12 space-y-0 md:space-y-0 md:flex-row">
        {/* Left Item */}
        <div className="flex flex-col mb-32 md:w-1/2">
          <h1 className="max-w-md text-4xl font-bold text-center md:text-left mb-2">
          Indian Aviation Academy
          </h1>
          <h2 className="max-w-md text-2xl font-bold text-center md:text-left mb-2">
           Nurturing Aviation for the Future
          </h2>
          <p className="max-w-sm text-center text-darkGrayishBlue md:text-left">
          Indian Aviation Academy (IAA), is the joint training academy of the Airports Authority of India (AAI), Director General of Civil Aviation (DGCA) and Bureau of Civil Aviation Security (BCAS). Its history can be traced back to year 1986, when the Institute of Airport Management started its operations from Patterson Farm House, located near Indira Gandhi International Airport.
          </p>
          <div className="flex justify-center md:justify-start mt-6">
            <Link
              to="#"
              className="p-3 px-6 pt-2 text-white bg-[#22409A] rounded-full baseline hover:bg-brightRedLight"
            >
              Start Learning
            </Link>
          </div>
        </div>
      </div>
        <div className="w-full">
          <img className='h-[65%] w-[100%]' src="../src/assets/images/airplane-image.png" alt="image" />
        </div>
    </section>
  );
};

export default Hero;
