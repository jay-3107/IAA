import { Link } from 'react-router-dom';

import avatarAnisha from '../assets/images/shree_sanjiv_kumar.png';
import avatarAli from '../assets/images/avatar-ali.png';
import avatarRichard from '../assets/images/avatar-richard.png';

const Testimonial = () => {
  return (
    <section id="testimonials">
      {/* Container to heading and testm blocks */}
      <div className="max-w-6xl px-5 mx-auto mt-32 text-center">
        {/* Heading */}
        <h2 className="text-4xl font-bold text-center">
        Vision Statement
        </h2>
        {/* Testimonials Container */}
        <div className="flex flex-col mt-24 md:flex-row md:space-x-6">
          {/* Testimonial 1 */}
          <div className="flex flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:w-1/3">
            <img src={avatarAnisha} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Shri Sanjeev Kumar</h5>
            <p className="text-sm text-darkGrayishBlue">
              “Shri Sanjeev Kumar, an IAS officer of the 1993 batch (Maharashtra Cadre), took charge as Chairman of the Airports Authority of India on April 7, 2021. He holds a bachelor's degree in Electronics & Communication Engineering from IIT Roorkee, a master’s in Communication Engineering from IIT Kanpur, and an MBA in Financial Management from Jamnalal Bajaj Institute of Management Studies, Mumbai University.

Before joining AAI, he was the State Commissioner for GST in Maharashtra and CMD of Maharashtra State Electricity Distribution Company Ltd (MSEDCL), where he significantly enhanced operational and financial performance. His previous roles include Joint Secretary and Mission Director for the "Housing for All" project (PMAY) and Director in the Ministry of Power, overseeing key programs like RGGVY and RAPDRP. He has also served in various departments within the Government of Maharashtra.”
            </p>
          </div>

          {/* Testimonial 2 */}
          <div className="hidden flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:flex md:w-1/3">
            <img src={avatarAli} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Dr. Srinivas Hanumankar</h5>
            <p className="text-sm text-darkGrayishBlue">
            Dr. Srinivas Hanumankar has taken over the charge of Member (Human Resources) from 10thMarch, 2023 on the Board of Airports Authority of India (AAI).Prior to this appointment, Shri Hanumankar was serving as Chief Personnel Officer in Indian Railways. As Member (Human Resources) of AAI, Dr. Srinivas will be the overall in-charge of coordinating and implementing Personnel and Industrial Relations policies, commercial management functions in the organization. Dr. Srinivas’s core areas of expertise range from Policy Making to Managing and Developing Human Resources and Relations of large organizations having diverse skill sets; Strategizing and Managing Change in large organizations through Training, Skilling/Upskilling, IT and Organization Development interventions, etc. He has worked in various capacities in three different Zones of the Indian Railways, each with around a lakh manpower strength and as Director General in one of the institutions of Ministry of Labour & Employment, GoI. Dr. Srinivas has represented India at various international forums and is also a recipient of the “Silver Star Award” presented by the Hon’ble President of India in the year 2019. Dr H. Srinivas holds a Bachelor (Hon's), Master's and Doctorate Degree in Earth Sciences, apart from a Post-Graduate Diploma in Management. He has had illustrious Academic and Professional careers and a vast array of accomplishments to his credit.
            </p>
          </div>

          {/* Testimonial 3 */}
          <div className="hidden flex-col items-center p-6 space-y-6 rounded-lg bg-veryLightGray md:flex md:w-1/3">
            <img src={avatarRichard} className="w-16 -mt-14" alt="" />
            <h5 className="text-lg font-bold">Shri Pankaj Malhotra</h5>
            <p className="text-sm text-darkGrayishBlue">
              “Shri Pankaj Malhotra has taken over the charge of the post of Member(Finance ) at the Airports Authority of India(AAI) on 9th November 2023. Prior to this appointment, Shri Pankaj Malhotra was serving as a Executive Director (Finance) at Central Electronics Limited, a Govt. of India enterprize under the Department of Scientific and Industrial Research(DSIR), Ministry of Science and Technology. ”
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
