import { Link } from 'react-router-dom';


const Hero = () => {
  return (
    <section id="hero">
      {/* Flex Container */}
      <div className="container flex flex-col-reverse items-center px-6 mx-auto mt-10 space-y-0 md:space-y-0 md:flex-row">
        {/* Left Item */}
        <div className="flex flex-col mb-32 space-y-12 md:w-1/2">
          <h1 className="max-w-md text-4xl font-bold text-center md:text-5xl md:text-left">
            Fly with Confidence. Fly with AAI.
          </h1>
          <p className="max-w-sm text-center text-darkGrayishBlue md:text-left">
            At the Airports Authority of India (AAI), we are committed to
            ensuring safe, efficient, and sustainable air travel across the
            nation. With state-of-the-art infrastructure, cutting-edge
            technology, and a customer-centric approach, we manage and operate
            airports that connect millions of passengers to their destinations.
            Discover our role in shaping the future of aviation in India.
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
