import { Link } from 'react-router-dom';

import avatarAnisha from '../assets/images/shree_sanjiv_kumar.png';
import avatarAli from '../assets/images/srini.png';
import avatarRichard from '../assets/images/shri.png';

const Testimonial = () => {
  return (
    <section id="testimonials">
      {/* Container to heading and testm blocks */}
      <div className="max-w-6xl px-5 mx-auto mt-32 text-center">
        {/* Heading */}
        <h2 className="text-4xl font-bold text-center">
        General Council
        </h2>
        {/* Testimonials Container */}
        <div className="flex flex-col mt-24 md:flex-row md:space-x-6">
          {/* Testimonial 1 */}
          <div className="flex flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:w-1/3">
            <img src={avatarAnisha} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Shri Sanjeev Kumar  </h5>
            <p className="text-sm text-darkGrayishBlue">
              “Shri Sanjeev Kumar, IAS 1993 batch (Maharashtra Cadre), became Chairman of the Airports Authority of India on April 7, 2021. He has degrees from IIT Roorkee, IIT Kanpur, and Jamnalal Bajaj Institute. Previously, he was State Commissioner for GST in Maharashtra and CMD of MSEDCL, and has held key roles in housing and power sectors.”
            </p>
          </div>

          {/* Testimonial 2 */}
          <div className="hidden flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:flex md:w-1/3">
            <img src={avatarAli} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Dr. Srinivas Hanumankar</h5>
            <p className="text-sm text-darkGrayishBlue">
              “Dr. Srinivas Hanumankar assumed the role of Member (Human Resources) at Airports Authority of India on March 10, 2023. Previously, he was Chief Personnel Officer at Indian Railways. With expertise in HR policy, change management, and development, Dr. Hanumankar has worked across multiple Indian Railways zones and received the 2019 Silver Star Award from the President of India. He holds advanced degrees in Earth Sciences and a Post-Graduate Diploma in Management..”
            </p>
          </div>

          {/* Testimonial 3 */}
          <div className="hidden flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:flex md:w-1/3">
            <img src={avatarRichard} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Shri Pankaj Malhotra</h5>
            <p className="text-sm text-darkGrayishBlue">
              “Shri Pankaj Malhotra has taken over the charge of the post of Member(Finance ) at the Airports Authority of India(AAI) on 9th November 2023. Prior to this appointment, Shri Pankaj Malhotra was serving as a Executive Director (Finance) at Central Electronics Limited, a Govt. of India enterprize under the Department of Scientific and Industrial Research(DSIR), Ministry of Science and Technology. .”
            </p>
          </div>
        </div>
        {/* Button */}
        <div className="my-16">
          <Link
            to="#"
            className="p-3 px-6 pt-2 text-white bg-[#22409A] rounded-full baseline hover:bg-brightRedLight"
          >
            Get Started
          </Link>
        </div>
      </div>
    </section>
  );
};

export default Testimonial;
