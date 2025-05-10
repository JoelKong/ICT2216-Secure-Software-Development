export default function Modal({ modal }) {
  return (
    <section
      className={`absolute w-full md:w-full h-7 top-5 z-10 flex justify-center rounded-md tracking-wide opacity-80 font-semibold text-gray-500 text-lg ${
        modal.type === "fail" ? "bg-red-400" : "bg-green-400"
      }`}
    >
      {modal.message}
    </section>
  );
}
