export function Button({ children, ...props }) {
    return <button {...props} className="bg-blue-500 text-white p-2 rounded-md">{children}</button>;
  }
  