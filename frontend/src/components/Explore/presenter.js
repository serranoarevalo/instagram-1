import React from 'react';
import PropTypes from 'prop-types';
import styles from './styles.scss';
import Loading from 'components/Loading';
import UserRow from 'components/UserRow';

const Explore = (props) => {
    if(props.loading){
        return <LoadingExplore />
    }else if(props.userList){
        return <RenderExplore {...props} />
    }
}

const LoadingExplore = props => {
    return(
    <div className = {styles.feed}>
        <Loading />
    </div>
)};

const RenderExplore = props => {
    return(
    <div className = {styles.Explore}>
        {props.userList.map(user => <UserRow big={true} user={user} key={user.id}/>)} 
    </div>
)};

Explore.propTypes = {
    loading: PropTypes.bool.isRequired,
    userList: PropTypes.array
}

export default Explore;