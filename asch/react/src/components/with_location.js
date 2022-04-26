// Copyright (c) 2022 David Chan
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import { useLocation } from 'react-router-dom';

export const withLocation = (Component) => {
    const Wrapper = (props) => {
        const location = useLocation();

        return <Component location={location} {...props} />;
    };

    return Wrapper;
};
